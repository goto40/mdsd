#ifndef WXEXT_wxImageFileDropTarget_H
#define WXEXT_wxImageFileDropTarget_H

#include "wxExt/wxImageReceiverInterface.h"
#include <wx/wx.h>
#include <wx/dnd.h>
#include <functional>

namespace wxExt {

    /** Drag and drop target for a wxImageReceiverInterface */
    class wxImageFileDropTarget : public wxFileDropTarget {
        wxImageReceiverInterface* ctrl;
    public:
        wxImageFileDropTarget(const wxImageFileDropTarget&)=delete;
        wxImageFileDropTarget& operator=(const wxImageFileDropTarget&)=delete;

        wxImageFileDropTarget(wxImageReceiverInterface* _ctrl) : ctrl(_ctrl) {}
        bool OnDropFiles(wxCoord, wxCoord, const wxArrayString& filenames) override {
            if (filenames.size()==1) {
                wxImage im(filenames[0].c_str());
                if (im.IsOk()) {
                    ctrl->SetImage(im);
                    return true;
                }
                else
                {
                    wxLogError("error reading file '%s'",
                            filenames[0].c_str());
                    return false;
                }
            }
            else {
                wxLogError("too many files receied via drag and drop (%d)",
                        static_cast<int>(filenames.size()));
                return false;
            }
        }
    };
    

}

#endif
