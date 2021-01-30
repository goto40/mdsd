#include "wxExt/wxImageViewer.h"
#include "wxExt/wxImagesZip.h"

namespace wxExt {
    template<class Viewer = wxImageViewer>
    class wxInputImageViewer : public wxPanel {
        Viewer* image_viewer = nullptr;
        wxComboBox* selector = nullptr;
        wxExt::wxImagesZip images_zip = {};

    void updateImageFromSelection() {
        auto name = std::string{selector->GetValue()};
        auto ptr = images_zip.LoadImage( name );
        image_viewer->SetImage( *ptr );
    }

    public:
        wxInputImageViewer(const wxInputImageViewer&) = delete;
        wxInputImageViewer& operator=(const wxInputImageViewer&) = delete;

        template<class ...T>
        wxInputImageViewer(T... params) :
                wxPanel(params...) {
            image_viewer = new Viewer(this, wxID_ANY);
            image_viewer->ActivateDrop();
            image_viewer->GetMenu().AddMyCommand("&Paste", [this](){
                image_viewer->Paste();
            });

            selector = new wxComboBox(this,
                wxID_ANY,
                wxEmptyString,
                wxDefaultPosition,
                wxDefaultSize,
                0,
                NULL,
                wxCB_READONLY
            );
            for(const auto &name : images_zip) {
                selector->Append(name);
            }
            selector->Bind(wxEVT_COMBOBOX, [this](auto &){
                updateImageFromSelection();
            });
            selector->SetSelection(0);
            updateImageFromSelection();

            wxBoxSizer *siz0 = new wxBoxSizer(wxVERTICAL);
            siz0->Add( image_viewer, 1, wxEXPAND );
            siz0->Add( selector, 0, wxEXPAND );

            SetSizer(siz0);
        }

        void Select(std::string name) {
            auto idx = selector->FindString(name, true); // case sensitive search (true)
            if (idx==wxNOT_FOUND) {
                throw std::runtime_error(name+"  not found");
            }
            selector->SetSelection(idx);
            updateImageFromSelection();
        }

        ~wxInputImageViewer() {
            std::cout << "Grmpf. End of life of wxInputImageViewer\n";
        }

        Viewer& GetImageViewer() {
            return *image_viewer;
        }
    };
}
