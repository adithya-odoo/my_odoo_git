/** @odoo-module **/
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import { formatInteger } from "@web/views/fields/formatters";
import { parseInteger  } from "@web/views/fields/parsers";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { Component, useState } from "@odoo/owl";

export class FloatToInteger extends Component {
   static template = 'web.FloatToInteger';
   static props = {
        ...standardFieldProps,
        formatNumber: { type: Boolean, optional: true },
        inputType: { type: String, optional: true },
        decimals: { type: Number, optional: true },

//        step: { type: Number, optional: true },
        digits: { type: Array, optional: true },
//        placeholder: { type: String, optional: true },
        humanReadable: { type: Boolean, optional: true },
    };
    static defaultProps = {
        formatNumber: true,
        inputType: "text",
        humanReadable: false,
    };

    setup() {
        console.log(this)
        this.state = useState({
            hasFocus: false,
        });
        this.inputRef = useInputField({
            getValue: () => this.formattedValue,
            refName: "numpadInteger",
            parse: (v) => this.parse(v),
        });
    }

    parse(value) {
    console.log("1")
       if(this.props.inputType === "number"){
        return Number(value)
       }
        else{
        console.log(typeof(value), "helllllllll")

         return parseInteger(value);
         }
    }
    get formattedValue() {
        console.log("2")
        if (
            !this.props.formatNumber ||
            (this.props.inputType === "number" && !this.props.readonly && this.value)
        ) {
            console.log("egfhjdvh")
            return this.value;
        }
        if (this.props.humanReadable && !this.state.hasFocus) {
            console.log("ffytfytyt")
            return formatInteger(this.value, {
                digits: this.digits,
                humanReadable: true,
                decimals: this.props.decimals,
            });
        } else {
            console.log("edjhg3du")
            console.log(typeof(this.value))
            return formatInteger(this.value, { digits: this.digits, humanReadable: false });
        }
    }

    get value() {

        console.log("3")
        return this.props.record.data[this.props.name];
    }
}

export const FloatToIntegers = {
    component: FloatToInteger,
    displayName: _t("Integer"),
    supportedTypes: ["float"],
    isEmpty: () => false,
    extractProps: ({ attrs, options }) => {
        return {
            formatNumber:
                options?.enable_formatting !== undefined
                    ? Boolean(options.enable_formatting)
                    : true,
            inputType: options.type,
        };
    },
};
registry.category("fields").add("float_to_integer", FloatToIntegers);
