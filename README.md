Source code for my Hexo blog about astronomy at http://siyu.china-vo.org.

```
hexo server
```

I'm using notion as my main note taking software. Posts here may be written in notion, and then exported as markdown / HTML for hexo.


To update the deployment on cosmostation, first `hexo generate`, then zip all content under public except CE4 and 2020 folder. Upload to backend and decompress.

NOTE:
- Use Notion exported HTML
  - Copy paste the HTML content to the post md, enclosed with {% notion_html %} {% end_notion_html %}
  - Rename image path to exclude file prefix and replace url encoded white spaces (%20)
  - Images imported this way won't show in the home page, make sure they're only displayed in the post page
- Images
  - With fancybox and lazy load, resizing can only be done with 
    ```
    <img src="img.png" title="img" width="200px" height="300px">
    ```
    it won't show in the home page