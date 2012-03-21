// Wrap code in an self-executing anonymous function and 
// pass jQuery into it so we can use the "$" shortcut without 
// causing potential conflicts with already existing functions.
(function($) {

    var validation = function() {

        var rules = {  // Private object

            name : {
                check: function(value) {
                    if(value) {
                        return testPattern(value, "^[-A-Za-z' .]*$");
                    }
                    return true;
                },
                msg: "Invalid"
            },

            email : {
               check: function(value) {

                   if(value) {
                       return testPattern(value,"[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])");
                   }
                   return true;
               },
               msg : "Invalid"
            },

            phone : {
               check: function(value) {

                   if(value) {
                       return testPattern(value,"^[- +0-9]{4,16}$");
                   }
                   return true;
               },
               msg : "Invalid"
            },

            required : {

               check: function(value) {

                   if(value) {
                       return true;
                   }
                   else {
                       return false;
                   }
               },
               msg : "Required field"
            }
        };
        var testPattern = function(value, pattern) {   // Private Method

            var regExp = new RegExp(pattern,"");
            return regExp.test(value);
        };
        return { // Public methods

            addRule : function(name, rule) {

                rules[name] = rule;
            },
            getRule : function(name) {

                return rules[name];
            }
        };
    };
    //A new instance of our object in the jQuery namespace.
    $.validation = new validation();

    var Form = function(form) {

        var fields = [];
        // Get all input elements in form
        $(form[0].elements).each(function() {
            var field = $(this);
            // We're only interested in fields with a validation attribute
            if(field.attr('validation') !== undefined) {
                fields.push(new Field(field));
            }
        });
        this.fields = fields;
    };

    var Field = function(field) {
        this.field = field;
        this.valid = false;
        this.attach("change");
    };

    Field.prototype = {
        // Method used to attach different type of events to
        // the field object.
        attach : function(event) {

            var obj = this;
            if(event == "change") {
                obj.field.bind("change",function() {
                    return obj.validate();
                });
            }
            if(event == "keyup") {
                obj.field.bind("keyup",function(e) {
                    return obj.validate();
                });
            }
        },

        // Method that runs validation on a field
        validate : function() {

            // Create an internal reference to the Field object. 
            var obj = this, 
                // The actual input, textarea in the object
                field = obj.field, 
                // A field can have multiple values to the validation
                // attribute, seprated by spaces.
                types = field.attr("validation").split(" "),
                error;

            // Iterate over validation types
            for (var type in types) {

                // Get the rule from our validation object.
                var rule = $.validation.getRule(types[type]);
                if(!rule.check(field.val())) {

                    field.addClass("error");
                    error = rule.msg;
                    break;
                }
            }
            if (error){                
                field.attr("value", "");     

                obj.valid = false;
            } 
            // No errors
            else {
                field.removeClass("error");
                obj.valid = true;
            }
        }
    };

    Form.prototype = {
        validate : function() {

            for(field in this.fields) {

                this.fields[field].validate();
            }
        },
        isValid : function() {

            for(field in this.fields) {

                if(!this.fields[field].valid) {

                    // Focus the first field that contains
                    // an error to let user fix it. 
                    this.fields[field].field.focus();

                    // As soon as one field is invalid
                    // we can return false right away.
                    return false;
                }
            }
            return true;
        }
    };

    $.extend($.fn, {

        validation : function() {

            if ($(this).length > 0){
                var validator = new Form($(this));
                $.data($(this)[0], 'validator', validator);

                $(this).bind("submit", function(e) {

                    validator.validate();
                    if(!validator.isValid()) {

                        e.preventDefault();
                    }
                });
            }
        },
        validate : function() {

            var validator = $.data($(this)[0], 'validator');
            validator.validate();
            return validator.isValid();
        }
    });

})(jQuery); 
// Again, we're passing jQuery into the function 
// so we can use $ without potential conflicts.
