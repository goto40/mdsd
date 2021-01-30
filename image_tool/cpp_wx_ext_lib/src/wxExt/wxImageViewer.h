#ifndef WXEXT_wxImageViewer_H
#define WXEXT_wxImageViewer_H

#include "wxExt/wxImageReceiverInterface.h"
#include "wxExt/wxImageFileDropTarget.h"
#include "wxExt/wxMyMenu.h"
#include "wxExt/wxMouseHelper.h"

#include <my_image_lib/image.h>
#include <my_image_lib/tools.h>
#include <mdsd_item_support.h>

#include <wx/wx.h>
#include <wx/clipbrd.h>
#include <memory>
#include <unordered_set>

namespace wxExt {

    struct wxSelectionListener {
        virtual void SetSelection(const wxRect&)=0;
        virtual void AddSelectionListener(wxSelectionListener &sl)=0;
        virtual void LinkViewer(wxSelectionListener &sl)=0;
        virtual ~wxSelectionListener() {}
    };
    
    struct BoolSetter {
        bool &b;
        BoolSetter(bool &_b) : b(_b) { b=true; }
        ~BoolSetter() { b=false; }
    };
    
    void gray2im(const my_image_lib::GrayImage& gray, wxImage& im) {
        // prepare
        mdsd::check_array_sizes_and_variants(gray);
        im.Create(gray.w, gray.h);
        float minv = my_image_lib::min(gray);
        float maxv = my_image_lib::max(gray);
        float diff = maxv-minv;
        if (std::abs(diff) < 1e-6) diff=1;
        // copy data
        unsigned char* data = im.GetData();
        for (size_t p=0;p<gray.w*gray.h;p++) {
            float g = (gray.pixel[p]-minv)/diff*255.0;
            unsigned char v = 0;
            if (g>254.5) {
                v = 255;
            }
            else if (g>=0) {
                v = static_cast<unsigned char>(g+0.5);
            }
            data[p*3+0] = v;
            data[p*3+1] = v;
            data[p*3+2] = v;
        }
    }
    void im2gray(const wxImage& im, my_image_lib::GrayImage& gray) {
        // prepare
        gray.w = im.GetWidth();
        gray.h = im.GetHeight();
        mdsd::adjust_array_sizes_and_variants(gray);
        // copy data
        unsigned char* data = im.GetData();
        for (size_t p=0;p<gray.w*gray.h;p++) {
            float v = (static_cast<float>(data[p*3+0])
                + static_cast<float>(data[p*3+1])
                + static_cast<float>(data[p*3+2]))/3.0/255.0;
            gray.pixel[p] = v;
        }
    }

    /** A simple image viewer with drag and drop functionality, zoom... */
    class wxImageViewer: public wxControl, public wxImageReceiverInterface, public wxSelectionListener {
        wxImage image = wxImage(wxSize(1,1));
        std::unique_ptr<wxMouseHelper> mouse;
        wxRect selection{0,0,1,1};
        wxSize displayed_size{1,1};
        wxMyMenu* mymenu;
        std::unordered_set<wxSelectionListener*> selectionListeners={};
        bool selectionListenerRecursionControl=false;
     public:
        wxImageViewer(const wxImageViewer &) = delete;
        wxImageViewer& operator=(const wxImageViewer &) = delete;
        template<class ...T>
        wxImageViewer(T... params) :
                wxControl(params...),
                mouse{std::make_unique<wxMouseHelper>(this)},
                mymenu(new wxMyMenu{}) {
            SetMinSize( wxSize(320,200) );
            Bind(wxEVT_PAINT, [=](wxPaintEvent &evt) { OnPaint(evt); });

            mymenu->AddMyCommand("&Reset Zoom", [this](){
                SetSelection( wxRect(0,0,image.GetWidth(),image.GetHeight()) );
            });

            // mouse interaction
            auto lambda_draw_selection = [this](const wxRect &rect){
                //std::cout << "draw "<< rect.x << "," << rect.y << "-"<< rect.width << "," << rect.height << "\n";
                wxClientDC dc(this);
                dc.SetPen(*wxYELLOW_PEN);
                dc.SetBrush(wxNullBrush);
                dc.SetLogicalFunction(wxINVERT);
                dc.DrawRectangle(rect);
            };
            mouse->eraseFunction = lambda_draw_selection;
            mouse->drawFunction = lambda_draw_selection;
            mouse->rectSelectedFunction = [this](const wxRect &rect){
                auto new_selection=rect;
                int x1 = new_selection.GetX()*selection.GetWidth()/displayed_size.x + selection.GetX();
                int y1 = new_selection.GetY()*selection.GetHeight()/displayed_size.y + selection.GetY();
                int x2 = x1 + 1 + new_selection.GetWidth()*selection.GetWidth()/displayed_size.x;
                int y2 = y1 + 1 + new_selection.GetHeight()*selection.GetHeight()/displayed_size.y;

                if (x2>x1 && y2>y1) {
                    SetSelection( wxRect(x1,y1,x2-x1, y2-y1) );
                }
            };
            mouse->rightClickFunction = [this](const wxPoint) {
                PopupMenu(mymenu);
            };
        }

        ~wxImageViewer() {
            std::cout << "Argh. ImageViewer deleted...\n";
        }

        wxMyMenu& GetMenu() {
            return *mymenu;
        }

        void SetImage(const wxImage &im) override {
            image = im;
            SetSelection( wxRect(0,0,im.GetWidth(),im.GetHeight()) );
        }
        
        void SetSelection(const wxRect &s) override {
            if (!selectionListenerRecursionControl) {
                BoolSetter setter(selectionListenerRecursionControl);

                int x1 = std::min( image.GetWidth()-1, std::max( 0, s.GetX() ));
                int y1 = std::min( image.GetHeight()-1, std::max( 0, s.GetY() ));
                int x2 = std::min( image.GetWidth(), std::max( 0, x1 + s.GetWidth() ));
                int y2 = std::min( image.GetHeight(), std::max( 0, y1 + s.GetHeight() ));

                if (x2>x1 && y2>y1) {
                    selection = wxRect(x1,y1,x2-x1, y2-y1);
                    for (auto &sl : selectionListeners) {
                            sl->SetSelection(s);
                    }
                    Refresh();
                }
            }
        }
        
        void AddSelectionListener(wxSelectionListener &sl) override {
            selectionListeners.insert(&sl);
        }
        void LinkViewer(wxSelectionListener &sl) override {
            if (!selectionListenerRecursionControl) {
                BoolSetter setter(selectionListenerRecursionControl);
                AddSelectionListener(sl);
                sl.LinkViewer(*this);
            }
        }

        bool Paste() {
            bool ret = false;
            if (wxTheClipboard->Open())
            {
                if (wxTheClipboard->IsSupported( wxDF_BITMAP ))
                {
                    std::cout << "found image in clipboard\n";
                    wxBitmapDataObject data;
                    wxTheClipboard->GetData( data );
                    SetImage( data.GetBitmap().ConvertToImage() );
                    ret = true;
                }
                else {
                    std::cout << "not found image in clipboard\n";
                }
                wxTheClipboard->Close();
            }
            return ret;
        }

        void ActivateDrop() {
            SetDropTarget(new wxExt::wxImageFileDropTarget{this});
        }

        virtual void OnPaint(wxPaintEvent &) {
                wxPaintDC dc(this);
                displayed_size = dc.GetSize();
                auto origin = dc.GetDeviceOrigin();

                // if widget is too wide
                if (displayed_size.x*selection.GetHeight() > selection.GetWidth()*displayed_size.y) {
                    displayed_size.x = selection.GetWidth()*displayed_size.y/selection.GetHeight();
                }
                else {
                    displayed_size.y = selection.GetHeight()*displayed_size.x/selection.GetWidth();
                }

                wxBitmap bitmap;
                get_sub_image(selection, bitmap);
                dc.DrawBitmap(bitmap, origin);
        }

        virtual void get_sub_image(const wxRect &selection, wxBitmap &sel) {
            sel = wxBitmap(image.GetSubImage(selection).Scale(displayed_size.x, displayed_size.y));
        }
    };

    /** A simple image viewer with drag and drop functionality, zoom... */
    class wxGrayImageViewer: public wxImageViewer {
        my_image_lib::GrayImage gray = {};
        std::vector<std::function<void(wxGrayImageViewer& v)>> callbacks = {};
     public:
        wxGrayImageViewer(const wxImageViewer &) = delete;
        wxGrayImageViewer& operator=(const wxImageViewer &) = delete;
        template<class ...T>
        wxGrayImageViewer(T... params) : wxImageViewer(params...) {
        }

        void BindOnImageChanged(std::function<void(wxGrayImageViewer& v)> f) {
            callbacks.push_back(f);
            f(*this);
        }

        void SetImage(const wxImage &im) override {
            im2gray(im, gray);
            SetImage(gray);
        }
        virtual void SetImage(const my_image_lib::GrayImage &gray) {
            wxImage im;
            gray2im(gray, im);
            wxImageViewer::SetImage(im);

            for(auto f: callbacks) {
                f(*this);
            }
        }
        
        const my_image_lib::GrayImage& GrayImage() {
            return gray;
        }

    };


}

#endif
