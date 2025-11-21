/**
 * Project:     conneCTION
 * Name:        static/src/controllers/editor_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-19
 * Description: EditorJS Controller
 */

import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  static targets = ["input", "holder"];
  static values = { readOnly: { type: Boolean, default: false } };

  connect() {
    this.#setupEditor();
  }

  #setupEditor() {
    Promise.all([import("@editorjs/editorjs"), this.#configureTools()]).then(([{ default: EditorJS }, tools]) => {
      this.editor = new EditorJS({
        tools,
        holder: this.holderTarget,
        data: JSON.parse(this.inputTarget.value),
        placeholder: this.inputTarget.placeholder,
        onChange: async (api, event) => {
          const data = await api.saver.save();
          this.inputTarget.value = JSON.stringify(data);
          this.dispatch("change", { detail: { data } });
        },
      });
    });
  }

  async #configureTools() {
    const [
      { default: header },
      { default: delimiter },
      { default: embed },
      { default: list },
      { default: quote },
      { default: table },
      { default: code },
      { default: underline },
      { default: textVariantTune },
    ] = await Promise.all([
      import("@editorjs/header"),
      import("@editorjs/delimiter"),
      import("@editorjs/embed"),
      import("@editorjs/nested-list"),
      import("@editorjs/quote"),
      import("@editorjs/table"),
      import("@editorjs/code"),
      import("@editorjs/underline"),
      import("@editorjs/text-variant-tune"),
    ]);
    return {
      header,
      delimiter,
      list,
      quote,
      table,
      code,
      underline,
      textVariantTune,
      embed: {
        class: embed,
        config: {
          services: {
            youtube: true,
            imgur: true,
            pintrest: true,
            scratch: {
              regex: /https?:\/\/scratch.mit.edu\/projects\/(\d+)/,
              embedUrl: "https://scratch.mit.edu/projects/<%= remote_id %>/embed",
              html: "<iframe height='300' scrolling='no' frameborder='no' allowtransparency='true' allowfullscreen='true' style='width: 100%;'></iframe>",
            },
          },
        },
      },
    };
  }
}
