# interaktiv.templates

The Plone backend add-on for [@interaktivgmbh/volto-templates](https://github.com/interaktivgmbh/volto-templates)

## Features

- Provides `TemplatesContainer` content type for organizing templates
- Provides `Template` content type with support for Volto blocks and thumbnail images
- REST API service `@templates-container` to find the nearest template container for a given content URL
- Extended `@types` service that injects template blocks into content type schemas
- Catalog indexer for template thumbnails
- Restricted workflow ensuring templates are only visible to authorized users

## Installation

Install interaktiv.templates with `pip`:

```shell
pip install interaktiv.templates
```

This addon requires the [@interaktivgmbh/volto-templates](https://github.com/interaktivgmbh/volto-templates) package to be installed on your Volto frontend.

## Content Types

### TemplatesContainer

A container for organizing templates. Can only contain `Template` items.

- Permissions restricted to Site Administrators and Managers
- Supports Volto blocks for content

### Template

Individual template instances with pre-configured block layouts.

| Field | Type | Description |
|-------|------|-------------|
| `template_description` | TextLine | Short description of the template |
| `template_thumbnail` | NamedBlobImage | Visual thumbnail for template preview |

Templates support all standard Volto blocks and can define default block configurations that are applied when creating new content from the template.

## REST API Services

### @templates-container

Returns all template containers and identifies the nearest one to a given content URL.

**Request:**
```
GET /@templates-container?url=/path/to/content
```

**Response:**
```json
{
  "containers": [
    {
      "title": "My Templates",
      "id": "templates",
      "url": "http://localhost:8080/Plone/templates",
      "path": "/Plone/templates"
    }
  ],
  "nearest_container": "http://localhost:8080/Plone/templates"
}
```

### @types (Extended)

The standard `@types` endpoint is extended to support template-based content creation. When a `template` parameter is provided, the response schema includes the template's default blocks.

**Request:**
```
GET /@types/Document?template=<template-uid>
```

**Response:**
Returns the Document schema with `blocks` and `blocks_layout` properties pre-populated from the template. Each block receives a new UUID to ensure uniqueness.

## Permissions

| Permission | Roles |
|------------|-------|
| `interaktiv.templates.AddTemplate` | Site Administrator, Manager |
| `interaktiv.templates.AddTemplatesContainer` | Site Administrator, Manager |

## Workflow

Templates use a simple internal workflow with a single `published_internally` state. Access is restricted to:
- Owner
- Site Administrator
- Manager

## Contribute

- [Issue tracker](https://github.com/interaktivgmbh/interaktiv.templates/issues)
- [Source code](https://github.com/interaktivgmbh/interaktiv.templates/)

### Prerequisites

- An [operating system](https://6.docs.plone.org/install/create-project-cookieplone.html#prerequisites-for-installation) that runs all the requirements mentioned
- [uv](https://6.docs.plone.org/install/create-project-cookieplone.html#uv)
- [Make](https://6.docs.plone.org/install/create-project-cookieplone.html#make)
- [Git](https://6.docs.plone.org/install/create-project-cookieplone.html#git)
- [Docker](https://docs.docker.com/get-started/get-docker/) (optional)

### Development Installation

1. Clone this repository:

    ```shell
    git clone git@github.com:interaktivgmbh/interaktiv.templates.git
    cd interaktiv.templates
    ```

2. Install the code base:

    ```shell
    make install
    ```

3. Start the Plone instance:

    ```shell
    make start
    ```

### Running Tests

```shell
make test
```

### Add features using `plonecli` or `bobtemplates.plone`

This package provides markers compatible with [`plonecli`](https://github.com/plone/plonecli) and [`bobtemplates.plone`](https://github.com/plone/bobtemplates.plone).

```shell
make add content_type   # Add a new content type
make add behavior       # Add a new behavior
```

## License

The project is licensed under GPLv2.

## Credits and acknowledgements

Generated using [Cookieplone (0.9.10)](https://github.com/plone/cookieplone) and [cookieplone-templates (dd13073)](https://github.com/plone/cookieplone-templates/commit/dd13073d34447056d6992461d8da29447d62c029) on 2026-01-20 13:56:23.415182. A special thanks to all contributors and supporters!
