class SearchIndex {
  data() {
    return { permalink: "/search-index.json", eleventyExcludeFromCollections: true };
  }
  render(data) {
    const items = (data.collections.wallpapers || []).map((item) => ({
      title: item.data.title,
      url: item.url,
      category: item.data.category,
      type: item.data.type,
      tags: item.data.tags_list || [],
      thumb: item.data.image_thumb || item.data.video_poster,
    }));
    return JSON.stringify(items);
  }
}
module.exports = SearchIndex;
