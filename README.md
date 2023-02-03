# openstack-openapi-schemas

A collection of OpenAPI v3.1 schemas for OpenStack APIs.

> **Warning**
> This is very much a work in progress and massively incomplete. You probably don't want to use this.

## Supported APIs

* Keystone v3

## How do I use this?

Because these are OpenAPI 3.1 specs, you can use any tool that supports OpenAPI 3.1. There are [many, many such
tools](https://openapi.tools/).

One good option is [rest.sh](https://rest.sh/). If you don't have this installed already, you should do so now.

```shell
go install github.com/danielgtaylor/restish@latest
```

Once installed, configure the API using a `~/.restish/apis.json` file, as described in the [configuration
guide](https://rest.sh/#/configuration?id=loading-from-files-or-urls).

```json
{
  "keystone": {
    "base": "http://devstack.local/identity",
    "spec_files": ["/path/to/openstack-openapi-schemas/keystone/keystone-v3.yaml"]
  }
}
```

> **Note**
> You can always modify `/etc/hosts` to configure e.g. `devstack.local` if running locally.

You can then interact with the chosen API using the `restish` CLI.

```shell
restish keystone --help
```

For example, you can view the index page.

```shell
restist keystone -H Accept:application/json index
```

> **Note**
> The `-H Accept:application/json` parameter is necessary with Keystone to prevent it returning
> [JSON-Home](https://datatracker.ietf.org/doc/html/draft-nottingham-json-home-06)-formatted responses.

For validation, [https://quobix.com/vacuum/](vacuum) is a fast, go-based OpenAPI validator.
