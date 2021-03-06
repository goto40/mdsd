/*
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

struct X {
    int &v;
    X(int &__v) : v(__v) {}
};

int main() {
    int v=1;
    X x(v);
    const X& c=x;
    c.v=2;     // references are handled like pointers here!! (const correctness)
}

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
*/

#include <iostream>
#include <string>
#include <thread>

#include "wxExt/wxInputImageViewer.h"
#include "wxExt/wxImagesZip.h"
#include <wx/wx.h>
#include <wx/clipbrd.h>

#include <my_image_lib/tools.h>
#include <my_image_lib/Tictoc.h>

#include <mdsd/item_support.h>
#include <mdsd/virtual_struct.h>
#include <mdsd/virtual_attribute_support.h>

#include <wx/propgrid/propgrid.h>
#include "my_image_lib/background_subtraction/AlgoBackgroundSubtractionImpl.h"

namespace {
    struct InitThingsForWxExt {
        InitThingsForWxExt() {
            wxInitAllImageHandlers();
        }
    } ___initThingsForWxExt;
}

template<class META>
class wxMessageAttributeProperty : public wxPGProperty
{
    typename META::STRUCT &s;
public:
    wxMessageAttributeProperty(typename META::STRUCT &__s)
        : wxPGProperty(META::__name(), META::__name()), s(__s)
    {
        SetValue( wxString{mdsd::AttributeWrapper<META>{s}.to_string()} );
    }
    virtual ~wxMessageAttributeProperty() { }
    const wxPGEditor* DoGetEditorClass() const { return wxPGEditor_TextCtrl; }
    wxString ValueToString( wxVariant&, int) const override
    {
        auto ret = mdsd::AttributeWrapper<META>{s}.to_string();
        //std::cout << /*variant.GetString() <<*/ " *** ret=" << ret << "\n";
        return ret;
    }
    bool StringToValue( wxVariant& variant, const wxString& text, int ) const override
    {
        typename META::STRUCT backup = s;
        const char* t = text;
        try {
            mdsd::AttributeWrapper<META>{s}.from_string(t);
            mdsd::adjust_array_sizes_and_variants(s);
        }
        catch(std::exception &e) {
            std::cout << "ERROR: "<< e.what() << "\n";
            //wxLog(e.what());
            s = backup;
            return false;
        }
        //std::cout << /*variant.GetString() <<*/ " *** set=" << mdsd::AttributeWrapper<META>{s}.to_string() << "\n";
        variant = text;
        return true;
    }
protected:
};

//algo::BackgroundDetectionParameter x;
template<class MESSAGE>
struct wxMessageEditor : wxPanel {
    MESSAGE parameter={};
    wxPropertyGrid *pg = nullptr;

    std::vector<std::function<void(const MESSAGE&)>> callbacks = {};

    struct SetterHelper {
        wxPropertyGrid *pg;
        template<class META>
        void visit(MESSAGE& m) {
            //std::cout << "Append(" << META::__name() << "...)\n";
            pg->Append( new wxMessageAttributeProperty<META>{m} );
        }
    };

    struct CheckerHelper {
        wxPropertyGrid *pg;
        bool ok=true;
        template<class META>
        void visit(MESSAGE& m) {
            auto ptr = pg->GetPropertyByName( META::__name() );
            if (ptr!=nullptr) {
                if (ptr->GetValue() != wxString( mdsd::AttributeWrapper<META>{m}.to_string() ) ) {
                    ok = false;
                }
            }
            else {
                ok = false;
            }
        }
    };

    void __on_content_changed() {
        CheckerHelper helper{pg};
        accept( helper, parameter );
        //std::cout << "changed "<< helper.ok <<".\n";
        if (!helper.ok) {
            RefreshData();
        }
        for(auto f: callbacks) {
            f(parameter);
        }
    }

    template<class ...T>
    wxMessageEditor(T... params) : wxPanel(params...) {
        
        //std::cout << "**INIT** " << parameter.selector << "\n"; 
        pg = new wxPropertyGrid(this, wxID_ANY);

        wxBoxSizer *siz0 = new wxBoxSizer(wxVERTICAL);
        siz0->Add( new wxStaticText(this,wxID_ANY,MESSAGE::META::__name()), 0, wxEXPAND );
        siz0->Add( pg, 1, wxEXPAND );
        SetSizer(siz0);

        pg->Bind(wxEVT_PG_CHANGED, [this](auto &){ __on_content_changed(); });

        RefreshData();
    }

    wxMessageEditor(const wxMessageEditor&) = delete;
    wxMessageEditor& operator=(const wxMessageEditor&) = delete;

    void BindOnMessageChanged(std::function<void(const MESSAGE&)> f) { callbacks.push_back(f); }

    void RefreshData() {
        SetterHelper helper{pg};
        pg->Clear();
        accept( helper, parameter );
        Refresh();
    }
};

// wxWidgets application
struct MyApp : wxApp
{
    // main/init function
    bool OnInit() override {
        auto f        = new wxFrame(nullptr,wxID_ANY, "Simple Demo");
        auto ctrl     = new wxExt::wxInputImageViewer<wxExt::wxGrayImageViewer>(f, wxID_ANY);
        auto viewer1   = new wxExt::wxGrayImageViewer(f, wxID_ANY);
        auto viewer2   = new wxExt::wxGrayImageViewer(f, wxID_ANY);
        auto sizer    = new wxBoxSizer( wxHORIZONTAL );
        auto pg       = new wxMessageEditor<my_image_lib::background_subtraction::BackgroundSubtractionParameters>(f, wxID_ANY);

        pg->Refresh();

        ctrl->Select("zeitung.png");
        ctrl->GetImageViewer().LinkViewer(*viewer1);
        ctrl->GetImageViewer().LinkViewer(*viewer2);

        // copy image from clipboard on startup
        if (wxApp::argc==2) {
            std::cout << "opening "<< wxApp::argv[1] << "\n";
            wxBitmap data;
            if (data.LoadFile(( wxApp::argv[1] ))) {
                ctrl->GetImageViewer().SetImage( data.ConvertToImage() );
            }
            else {
                std::cout << "error opening "<< wxApp::argv[1] << "\n";
            }
        }

        sizer->Add(ctrl, 1, wxEXPAND);
        sizer->Add(viewer1, 1, wxEXPAND);
        sizer->Add(viewer2, 1, wxEXPAND);
        sizer->Add(pg, 1, wxEXPAND);
        f->SetSizerAndFit(sizer);

        auto compute = [viewer1,viewer2, ctrl, pg]() {
            auto &v = ctrl->GetImageViewer();
            std::cout << v.GrayImage().w << " x "
                << v.GrayImage().w << "\n";
            auto algo = my_image_lib::background_subtraction::AlgoBackgroundSubtraction::create();
            my_image_lib::background_subtraction::BackgroundSubtractionResults res;
            algo->set_params( pg->parameter );
            std::cout << "th=" << pg->parameter.threshold << "\n";
            algo->compute(v.GrayImage(), res);
            viewer1->SetImage( res.threshold );
            viewer2->SetImage( res.result );
        };
        ctrl->GetImageViewer().BindOnImageChanged([compute](auto &){ compute(); });
        pg->BindOnMessageChanged([compute](auto &){ compute(); });

        f->SetSize( wxSize{1000,600} );
        (void)f->Show(true);
        return true;
    }
};

// main-function etc.:
IMPLEMENT_APP(MyApp)
