/**
 * Project:     conneCTION
 * Name:        static/src/controllers/dialog_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-20
 * Description: Dialog Helper
 */

import { Controller } from "@hotwired/stimulus";

export default class extends Controller {
  toggleDialog({ params: { id, method = "showModal" } }) {
    const el = document.querySelector(`#${id}`);
    if (!el.open) {
      if (method === "showModal") el.showModal();
      else el.show();
    } else {
      el.close();
    }
  }
}
