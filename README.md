[![](https://img.shields.io/pypi/v/foliantcontrib.imagineui.svg)](https://pypi.org/project/foliantcontrib.imagineui/) [![](https://img.shields.io/github/v/tag/imagineui/foliantcontrib.imagineui.svg?label=GitHub)](https://github.com/imagineui/foliantcontrib.imagineui)

# ImagineUI for Foliant

ImagineUI is a tool that supports developing wireframes in a localized human-readable format.

This preprocessor allows using `<imagineui>` macros in Foliant

## Installation

Before using ImagineUI, you need to install [Node.js](https://nodejs.org/en/).

ImagineUI preprocessor code is written in Python, but it uses a JavaScript package. This script is provided in ImagineUI package:

```bash
$ pip install foliantcontrib.imagineui
```

ImagineUI uses Puppeteer for rendering in background, which is a huge dependency, so to avoid downloading Chrome every time this preprocessor applies, it's advised to install `imagineui-cli` globally.

```bash
$ npm i -g imagineui-cli 
```

## Config

To enable the preprocessor, add `imagineui` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - imagineui
```

The preprocessor has a number of options with the following default values:

```yaml
preprocessors:
    - imagineui:
        version: global
        cache_dir: !path .imagineuicache
```

`version`
:   Version of the `imagineui-cli` package in NPM. "global" (default) will skip and will use either the version already installed globally or the latest version, which speeds up NPX significantly. 

`cache_dir`
:   Directory to store downloaded and resized images.

## Usage

To insert a wireframe image rendered by ImagineUI into your documentation, use `<imagineui>...</imagineui>` tags in Markdown source:

```markdown
<imagineui>
    Page: "Welcome screen"
    Block: "Header"
        Header "Mockup poetry"
    Block: "Flowers"
        Two columns
            Image "Roses are red,"
            Image "Violets are blue."
            Image "Your mockups are awesome,"
            Image "And so are you!"
    Block: "Footer"
        One row
            Button "Try ImagineUI"
            Button "Subscribe"
            Button "Contribute"
</imagineui>
```

ImagineUI preprocessor will replace such blocks with local image references.


## Acknowledgements
[BindSympli](https://github.com/foliant-docs/foliantcontrib.bindsympli) preprocessor was used as a starting point