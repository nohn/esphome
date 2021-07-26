from esphome import automation
import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import select
from esphome.const import (
    CONF_ID,
    CONF_INITIAL_VALUE,
    CONF_LAMBDA,
    CONF_OPTIONS,
    CONF_OPTIMISTIC,
    CONF_RESTORE_VALUE,
)
from .. import template_ns

TemplateSelect = template_ns.class_(
    "TemplateSelect", select.Select, cg.PollingComponent
)

CONF_SET_ACTION = "set_action"

CONFIG_SCHEMA = cv.All(
    select.SELECT_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(TemplateSelect),
            cv.Required(CONF_OPTIONS): cv.All(
                cv.ensure_list(cv.string_strict), cv.Length(min=1)
            ),
            cv.Optional(CONF_LAMBDA): cv.returning_lambda,
            cv.Optional(CONF_OPTIMISTIC): cv.boolean,
            cv.Optional(CONF_SET_ACTION): automation.validate_automation(single=True),
            cv.Optional(CONF_INITIAL_VALUE): cv.string_strict,
            cv.Optional(CONF_RESTORE_VALUE): cv.boolean,
        }
    ).extend(cv.polling_component_schema("60s")),
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await select.register_select(var, config, options=config[CONF_OPTIONS])

    if CONF_LAMBDA in config:
        template_ = await cg.process_lambda(
            config[CONF_LAMBDA], [], return_type=cg.optional.template(str)
        )
        cg.add(var.set_template(template_))

    else:
        if CONF_OPTIMISTIC in config:
            cg.add(var.set_optimistic(config[CONF_OPTIMISTIC]))
        if CONF_INITIAL_VALUE in config:
            cg.add(var.set_initial_value(config[CONF_INITIAL_VALUE]))
        if CONF_RESTORE_VALUE in config:
            cg.add(var.set_restore_value(config[CONF_RESTORE_VALUE]))

    if CONF_SET_ACTION in config:
        await automation.build_automation(
            var.get_set_trigger(), [(cg.std_string, "x")], config[CONF_SET_ACTION]
        )
