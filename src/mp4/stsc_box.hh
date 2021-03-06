#ifndef STSC_BOX_HH
#define STSC_BOX_HH

#include <string>
#include <vector>

#include "box.hh"

namespace MP4 {

class StscBox : public FullBox
{
public:
  struct Entry {
    uint32_t first_chunk;
    uint32_t samples_per_chunk;
    uint32_t sample_description_index;
  };

  StscBox(const uint64_t size, const std::string & type);

  /* accessors */
  uint32_t entry_count() { return entries_.size(); }
  std::vector<Entry> entries() { return entries_; }

  /* mutators */
  void set_entries(std::vector<Entry> entries);

  void print_box(const unsigned int indent = 0);

  void parse_data(MP4File & mp4, const uint64_t data_size);
  void write_box(MP4File & mp4);

private:
  std::vector<Entry> entries_;
};

} /* namespace MP4 */

#endif /* STSC_BOX_HH */
