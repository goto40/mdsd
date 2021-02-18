#ifndef WXEXT_wxMouseHelper_H
#define WXEXT_wxMouseHelper_H

#include <wx/wx.h>

namespace wxExt {

    constexpr double abs(const wxPoint &a) {
        return sqrt(a.x*a.x+a.y*a.y);
    }

    /** helper class to handle mouse drag/move/press actions of a control (passed to this object).
      * The behavior can be customized by overrinding the callback functions (std::function).
      */
    class wxMouseHelper {
        wxPoint p0{},p1{};
        bool isPressed=false;
        bool isDragging=false;
        void ldown(const wxPoint& p) {
            p0=p;
            isPressed=true;
            isDragging=false;
        }
        void rdown(const wxPoint& p) {
            rightClickFunction(p);
        }
        void move(const wxPoint& p) {
            if (isPressed) {
                if (isDragging) {
                    eraseFunction( wxRect(p0,p1) );
                }
                else if (abs(p-p0)>2) {
                    isDragging=true;
                }
                if (isDragging) {
                    drawFunction( wxRect(p0,p) );
                }
                p1=p;
            }
        }
        void lup(const wxPoint& p) {
            if (isDragging) {
                eraseFunction( wxRect(p0,p1) );
                rectSelectedFunction( wxRect(p0,p) );
            }
            else {
                pointSelectedFunction( p0 );
            }
            p1=p;
            isPressed=false;
            isDragging=false;
        }
    public:
        std::function<void(const wxRect&)>  drawFunction = [](const wxRect&){};
        std::function<void(const wxRect&)>  eraseFunction = [](const wxRect&){};
        std::function<void(const wxRect&)>  rectSelectedFunction = [](const wxRect&){};
        std::function<void(const wxPoint&)> pointSelectedFunction = [](const wxPoint&){};
        std::function<void(const wxPoint&)> rightClickFunction = [](const wxPoint&){};

        template<class WXC>
        wxMouseHelper(WXC* wxc) {
            wxc->Bind(wxEVT_RIGHT_DOWN, [=](wxMouseEvent &evt) { rdown(wxPoint{evt.m_x, evt.m_y}); });
            wxc->Bind(wxEVT_LEFT_DOWN,  [=](wxMouseEvent &evt) { ldown(wxPoint{evt.m_x, evt.m_y}); });
            wxc->Bind(wxEVT_LEFT_UP,    [=](wxMouseEvent &evt) { lup(wxPoint{evt.m_x, evt.m_y}); });
            wxc->Bind(wxEVT_MOTION,     [=](wxMouseEvent &evt) { move(wxPoint{evt.m_x, evt.m_y}); });
        }
    };

}

#endif
