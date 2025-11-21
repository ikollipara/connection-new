/**
 * Project:     conneCTION
 * Name:        static/src/controllers/combobox_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-14
 * Description: ComboBox Controller
 */

import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static values = {
    contentLocation: { type: String, default: undefined },
    contentPosition: { type: String, default: "absolute" },
  };

  #slimSelectModule = null;
  #canConnect = false;

  initialize() {
    Promise.allSettled([import("slim-select/styles"), import("slim-select")]).then(([_, slimSelect]) => {
      this.#slimSelectModule = slimSelect.value.default;
      this.#canConnect = true;
    });
  }

  connect() {
    this.#initializeSlimSelect();
  }

  disconnect() {
    this.slimSelect.destroy();
  }

  #initializeSlimSelect() {
    if (!this.#canConnect) {
      setTimeout(this.#initializeSlimSelect.bind(this));
    } else {
      this.slimSelect = new this.#slimSelectModule({
        select: this.element,
        settings: {
          contentLocation: document.querySelector(this.contentLocationValue),
          contentPosition: this.contentPositionValue,
        },
      });
    }
  }
}
