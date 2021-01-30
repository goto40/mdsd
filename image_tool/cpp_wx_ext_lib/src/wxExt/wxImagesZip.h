#ifndef WXEXT_WXIMAGESZIP_H
#define WXEXT_WXIMAGESZIP_H

#include <memory>
#include <unordered_map>
#include <string>
#include <vector>

#include <wx/zipstrm.h>
#include <wx/mstream.h>

namespace wxExt {

    class wxImagesZip {
        std::unique_ptr<wxMemoryInputStream> mem_in;
        std::unique_ptr<wxZipInputStream> zip_in;
        std::unordered_map<std::string, std::shared_ptr<wxZipEntry>> entries;
        std::vector<std::string> entry_names;
    public:
        wxImagesZip(const unsigned char* binary_data=nullptr, size_t len=0);
        wxImagesZip(const wxImagesZip&) = delete;
        wxImagesZip& operator=(const wxImagesZip&) = delete;

        size_t size() const { return entries.size(); }
        const std::string& operator[](size_t idx) const;
        std::shared_ptr<wxImage> LoadImage(const std::string& name);

        auto begin() const { return entry_names.begin(); }
        auto end() const { return entry_names.end(); }
    };

}

#endif
