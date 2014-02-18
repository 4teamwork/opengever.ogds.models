Introduction
============

This package contains the SQLAlchemy models for the OpenGever directory
service.

The purpose of making `opengever.ogds.models` its own package is to allow
other appliactions than OpenGever to use its models, for example the so called
"bridge" (a small Pyramid application).

Therefore `opengever.ogds.models` should not have any Plone dependencies (except
for testing, using the `[tests]` extra), but instead only depend on SQLAlchemy
and possibly other pure Python libraries.
