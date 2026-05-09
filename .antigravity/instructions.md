# Cosmostation Blog Structure and Writing Guide

## Overview
This repository (`siyu.china-vo.org` / `cosmostation`) is a static blog generated using **Hexo** (version 7.1.1). 
- **Theme**: `stun`
- **Language**: Chinese (`cn`)
- **Author**: Siyu Zhang
- **Package Manager Scripts**: 
  - `npm run server` (or `hexo server`): Local preview
  - `npm run build`: Generate static files
  - `npm run deploy`: Deploy the site

## Directory Structure
- `source/_posts/`: Contains all the blog posts (Markdown files) and their corresponding asset folders.
- `_config.yml`: Global Hexo configuration.
- `package.json`: Node dependencies, including some custom plugins like `hexo-notion-html`.

## Writing a New Post
When creating a new blog post, follow these rules:

1. **Post Location**: 
   All posts must be created in the `source/_posts/` directory as a Markdown file (`.md`).
   
2. **Asset Folder**: 
   The global config has `post_asset_folder: true` enabled. This means **for every new post file (e.g., `my-post.md`), you MUST create a folder with the exact same name** (e.g., `my-post/`) in the `source/_posts/` directory to store its images and other assets.

3. **Front-Matter**:
   Every post must start with a YAML front-matter block containing at least the `title`, `date`, and `tags`.
   ```yaml
   ---
   title: [Your Post Title]
   date: YYYY-MM-DD HH:mm:ss
   tags: 
    - [tag1]
    - [tag2]
   ---
   ```

4. **Images & Assets**:
   Place images inside the post's asset folder. You can embed them in the markdown using:
   - Standard Markdown: `![caption](image.png)`
   - Hexo Asset Image Tag: `{% asset_img image.png "caption" %}`

5. **Excerpts**:
   Use `<!-- more -->` to separate the summary/excerpt from the main content of the post. The text before this tag will be shown on the blog index page.

6. **Custom Elements**:
   - Note blocks (Stun theme / Hexo feature): 
     ```html
     {% note success default %}
     Your note content here
     {% endnote %}
     ```
