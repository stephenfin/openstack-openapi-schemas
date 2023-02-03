import argparse
import json

import openapi_core as openapi
from openapi_core.contrib.requests import (
    RequestsOpenAPIRequest,
    RequestsOpenAPIResponse,
)
from openapi_core.unmarshalling.schemas.factories import (
    SchemaUnmarshallersFactory,
)
from openapi_core.validation.request.validators import RequestValidator
from openapi_core.validation.response.validators import ResponseValidator
import openapi_schema_validator
import requests
import responses


class DateTimeFormatter:
    def validate(self, value) -> bool:
        # TODO: Implement
        return True

    def format(self, value) -> str:
        # TODO: Implement
        return value


schema_unmarshallers_factory = SchemaUnmarshallersFactory(
    openapi_schema_validator.OAS31Validator,
    custom_formatters={
        "date-time": DateTimeFormatter(),
    },
)


def validate(spec_path: str, req_path: str, rsp_path: str) -> None:
    spec = openapi.Spec.from_file_path(spec_path)

    with open(req_path) as fh:
        req_data = fh.read()

    with open(rsp_path) as fh:
        rsp_data = fh.read()

    with responses.RequestsMock() as rsps:
        session = requests.Session()
        rsps.add(
            responses.POST,
            "http://devstack.local/identity/v3/auth/tokens",
            body=rsp_data,
            status=200,
            content_type="application/json",
        )

        req = requests.Request(
            "POST",
            "http://devstack.local/identity/v3/auth/tokens",
            json=json.loads(req_data),
            headers=None,
        )
        rsp = session.send(req.prepare())

    openapi_req = RequestsOpenAPIRequest(req)
    openapi_rsp = RequestsOpenAPIResponse(rsp)

    # FIXME: This changes in the next version of openapi-core
    openapi.validate_request(
        spec,
        openapi_req,
        validator=RequestValidator(
            schema_unmarshallers_factory=schema_unmarshallers_factory,
        ),
    )
    openapi.validate_response(
        spec,
        openapi_req,
        openapi_rsp,
        validator=ResponseValidator(
            schema_unmarshallers_factory=schema_unmarshallers_factory,
        ),
    )

    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "spec",
        type=str,
        help="Path to spec",
    )
    parser.add_argument(
        "request",
        type=str,
        help="Path to stored request to validate against spec",
    )
    parser.add_argument(
        "response",
        type=str,
        help="Path to stored response to validate against spec",
    )
    args = parser.parse_args()
    validate(args.spec, args.request, args.response)
    return None


if __name__ == "__main__":
    main()
