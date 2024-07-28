# Configuration file for the Sphinx documentation builder.
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

import tomli

sys.path.insert(0, os.path.abspath(".."))


# Function to read version from pyproject.toml
def get_version_from_pyproject():
    pyproject_path = os.path.join(os.path.dirname(__file__), "..", "pyproject.toml")
    with open(pyproject_path, "rb") as pyproject:
        pyproject_data = tomli.load(pyproject)
    return pyproject_data["tool"]["poetry"]["version"]


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "langstring"
copyright = "Pedro Paulo F. Barcelos <p.p.favatobarcelos@utwente.nl>"
author = "Pedro Paulo F. Barcelos <p.p.favatobarcelos@utwente.nl>"

# Extract version and release from pyproject.toml
version = get_version_from_pyproject()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "autoapi.extension",
    "myst_parser",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",
    "sphinx_rtd_size",
    "sphinx_toolbox.sidebar_links",
]

autodoc_typehints = "description"
github_username = "pedropaulofb"
github_repository = "pedropaulofb/langstring"

autoapi_dirs = ["../langstring/"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_logo = "../resources/langstring-lib-logo.png"
html_theme_options = {"display_version": True}

sphinx_rtd_size_width = "100%"

html_css_files = [
    "logo_resize.css",
]
