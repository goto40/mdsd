#ifndef WXEXT_wxImageReceiverInterface_H
#define WXEXT_wxImageReceiverInterface_H

#include <wx/wx.h>

namespace wxExt {

    /** An interface to set an image */
    struct wxImageReceiverInterface {
        virtual void SetImage(const wxImage &im)=0;
        virtual ~wxImageReceiverInterface() {}
    };

}

#endif
