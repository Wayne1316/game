# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def model_edit_fields(model, exclue=list()):
    fields = [x.name for x in getattr(model, '_meta').fields if x.editable and not x.auto_created]
    [fields.remove(x) for x in exclue]
    return fields
