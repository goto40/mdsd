#include <wx/wx.h>
#include "wxExt/wxImagesZip.h"
#include "images_zip.h" // big data!

#include <cassert>
#include <iostream>
#include <vector>
#include <algorithm>

namespace wxExt {
    wxImagesZip::wxImagesZip(const unsigned char* binary_data, size_t len) : mem_in{}, zip_in{}, entries{}, entry_names{} {
        if (binary_data==nullptr) {
            binary_data = zip_data::res_images_zip;
            len = sizeof(zip_data::res_images_zip);
        }
        mem_in = std::make_unique<wxMemoryInputStream>(reinterpret_cast<const void*>(binary_data), len);
        zip_in = std::make_unique<wxZipInputStream>(*mem_in);

        std::shared_ptr<wxZipEntry> entry{new wxZipEntry()};
        while (entry.reset(zip_in->GetNextEntry()), entry.get() != NULL) {
            wxString name = entry->GetName();
            if (!entry->IsDir()) {
                //std::cout << "file: " << name << "\n";
                if (name.Lower().EndsWith(".png") || name.Lower().EndsWith(".jpg")) {
                    entries[std::string{name}] = entry;
                    entry_names.push_back(std::string{name});
                }
            }
        }
        std::sort( entry_names.begin(), entry_names.end() );
        assert( entry_names.size() == entries.size() );
    }

    const std::string& wxImagesZip::operator[](size_t idx) const {
        return entry_names.at(idx);
    }

    std::shared_ptr<wxImage> wxImagesZip::LoadImage(const std::string& name) {
        zip_in->OpenEntry(*entries[name]);
        if (!zip_in->CanRead()) {
            wxLogError(_T("Can not read zip entry '") + name + _T("'."));
            throw std::runtime_error("open error.");
        }

        // read data into mem
        size_t data_size = entries[name]->GetSize();
        std::vector<std::byte> data(data_size);

        zip_in->Read(static_cast<void*>(data.data()), data_size);
        if (zip_in->LastRead() != data_size) {
            wxLogError(_T("Can not read data for zip entry '") + name + _T("'."));
            throw std::runtime_error("read error.");
        }

        // read from mem into image (stream needs to be seekable)
        wxMemoryInputStream tmp_in(static_cast<void*>(data.data()), data_size);
        auto img = std::make_shared<wxImage>();
        if (img->LoadFile( tmp_in )) {
            return img;
        }
        else {
            wxLogError(_T("Error reading zip entry '") + name + _T("'."));
            throw std::runtime_error("load error.");
        }
    }
}
