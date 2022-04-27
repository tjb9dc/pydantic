import pytest

from pydantic import BaseModel, Extra


class ForbidExtraModel(BaseModel):
    class Config:
        extra = Extra.forbid


class Inner(ForbidExtraModel):
    core_field: str


class InnerChild(Inner):
    extra_field: str


class Outer(ForbidExtraModel):
    inner: Inner


def test_validation_from_constructor() -> None:
    # This test FAILS since the constructor does not validate
    with pytest.raises(Exception):
        Outer(inner=InnerChild(core_field='core_field', extra_field='extra_field'))


def test_validation_from_parse_obj() -> None:
    # This test SUCCEEDS since parse_obj recursively validates objects correctly
    outer_dict = {'inner': {'core_field': 'core_field', 'extra_field': 'extra_field'}}
    with pytest.raises(Exception):
        Outer.parse_obj(outer_dict)


def test_round_trip() -> None:
    # This test FAILS, but would change once test_validation_from_constructor() is fixed since it shouldn't be
    # possible to construct Outer this way. But it does fail currently and shows the inconsistency in validation
    outer_dict = Outer(inner=InnerChild(core_field='core_field', extra_field='extra_field')).dict()
    Outer.parse_obj(outer_dict)
