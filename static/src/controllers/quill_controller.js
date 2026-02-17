/**
 * Project:     conneCTION
 * Name:        static/src/controllers/quill_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-19
 * Description: Quill.js Editor
 */

import { Controller } from "@hotwired/stimulus";

/**
 * Quill Controller
 * --------------------------
 * A controller handling the initialization of the quill.js text editor.
 * Quill is used to handle comments and other, less intense writing.
 */
export default class extends Controller {
  static values = {
    // The name of the quill.js editor instance.
    // This is used to integrate with HTML forms.
    name: String,
    value: { type: String, default: "" },
    // Whether the contents should be considered read only.
    readOnly: { type: Boolean, default: false },
  };

  connect() {
    this.#setupQuill();
  }

  async #setupQuill() {
    // We dynamically import the modules to save on the initial bundle size.
    const styles = Promise.all([
      import("quill/dist/quill.core.css"),
      import("quill/dist/quill.bubble.css"),
    ]);
    const { default: Quill } = await import("quill");
    this.div = document.createElement("div");
    // This ensures that the styles are loaded before continuing.
    const _ = await styles;
    this.element.appendChild(this.div);

    this.quill = new Quill(this.div, {
      theme: "bubble",
      readOnly: this.readOnlyValue,
    });

    this.quill.clipboard.dangerouslyPasteHTML(this.valueValue, "silent");
  }

  handleFormUpdate(event) {
    const formSubmission = event.detail.formSubmission;
    console.log(formSubmission);
    formSubmission.body.append(this.nameValue, this.quill.getSemanticHTML());
  }
}
