/**
 * Project:     conneCTION
 * Name:        static/src/controllers/quill_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-19
 * Description: Quill.js Editor
 */

import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static values = { name: String, value: { type: String, default: "" }, readOnly: { type: Boolean, default: false } };

  connect() {
    this.#setupQuill();
  }

  async #setupQuill() {
    await import("quill/dist/quill.core.css");
    const { default: Quill } = await import("quill");
    this.div = document.createElement("div");
    this.element.appendChild(this.div);

    this.quill = new Quill(this.div, {
      theme: "bubble",
      readOnly: this.readOnlyValue,
      modules: {
        toolbar: [["bold", "italic", "underline", "strike"]],
        clipboard: true,
      },
    });

    this.quill.clipboard.dangerouslyPasteHTML(this.valueValue, "silent");
  }

  handleFormUpdate(event) {
    event.formData.append(this.nameValue, this.quill.getSemanticHTML());
  }
}
