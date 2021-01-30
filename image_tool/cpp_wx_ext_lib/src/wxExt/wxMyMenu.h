#ifndef WXEXT_WXMYMENU_H
#define WXEXT_WXMYMENU_H
#include <wx/wx.h>
#include <unordered_map>
#include <functional>

namespace wxExt {
    
    /** simple wrapper fro a wxmenu */
    class wxMyMenu : public wxMenu {
        std::unordered_map<wxMenuItem*, std::function<void(void)>> functions;
    public:
        template<class ...T>
        wxMyMenu(T... params) : wxMenu(params...), functions{} {
            Bind(wxEVT_COMMAND_MENU_SELECTED, [=](wxCommandEvent &evt){
                std::cout << "menu selected."<< evt.GetId() << "\n";
                auto mi = FindItem(evt.GetId());
                if (functions.find(mi)!=functions.end()) {
                    functions[mi]();
                }
            });
        }
        void AddMyCommand(wxString text, std::function<void(void)> f) {
            auto item = Append(wxID_ANY, text);
            functions[item] = f;
        }
    };
}

#endif
