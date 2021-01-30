#include <iostream>
#include <string>

#include "wxExt/wxInputImageViewer.h"
#include "wxExt/wxImagesZip.h"
#include <wx/wx.h>
#include <wx/clipbrd.h>

namespace {
    struct InitThingsForWxExt {
        InitThingsForWxExt() {
            wxInitAllImageHandlers();
        }
    } ___initThingsForWxExt;
}

// wxWidgets application
struct MyApp : wxApp
{
    // main/init function
    bool OnInit() override {
        auto f        = new wxFrame(nullptr,wxID_ANY, "Simple Demo");
        auto ctrl     = new wxExt::wxInputImageViewer<wxExt::wxImageViewer>(f, wxID_ANY);
        auto sizer    = new wxBoxSizer( wxVERTICAL );

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
        f->SetSizerAndFit(sizer);

        (void)f->Show(true);
        return true;
    }
};

// main-function etc.:
IMPLEMENT_APP(MyApp)
