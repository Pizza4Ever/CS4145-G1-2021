exports.Task = extend(TolokaHandlebarsTask, function (options) {
  TolokaHandlebarsTask.call(this, options);
}, {
  onRender: function() {
    var $el = $(this.getDOMElement());

    this._getFile = this.file.getFile;
    this.file.getFile = function() {
        this.focus();

        return this._getFile.apply(this.file, arguments);
    }.bind(this);

    const root = this.getDOMElement();


    const input = root.querySelectorAll('input');
    const button = root.querySelector('button');
    var order = [];
    console.log(button);
    console.log(input);
    function updateValue(e) {
        console.log(e);
        // this.disabled = true
        this.setAttribute("highlighted", "highlighted")
    }

    input.forEach((inp) => {
        console.log(inp);
        inp.addEventListener('click', updateValue);
    });




    function buttonEvent(e) {
        var imgs = [];
        input.forEach((item) => {
            if (item.hasAttribute("highlighted")) {
                item.removeAttribute("highlighted");
                item.setAttribute("selected", "selected");
                imgs.push(item.getAttribute("idx"));
                item.disabled = true
            }
        });
        order.push(imgs)
    }

    button.addEventListener('click', buttonEvent);

    console.log("test");
  },
  onDestroy: function() {
    // Task is completed. Global resources can be released (if used)
  }
});

function extend(ParentClass, constructorFunction, prototypeHash) {
  constructorFunction = constructorFunction || function () {};
  prototypeHash = prototypeHash || {};
  if (ParentClass) {
    constructorFunction.prototype = Object.create(ParentClass.prototype);
  }
  for (var i in prototypeHash) {
    constructorFunction.prototype[i] = prototypeHash[i];
  }
  return constructorFunction;
}
