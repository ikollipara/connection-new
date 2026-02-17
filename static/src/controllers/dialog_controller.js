/**
 * Project:     conneCTION
 * Name:        static/src/controllers/dialog_controller.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-20
 * Description: Dialog Helper
 */

import { Controller } from "@hotwired/stimulus";

/**
 * Dialog Controller
 * ------------------------
 * This controller allows dynamic access to modals.
 * This can be removed once everything is converted to
 * using the new (as of 2026) `commandfor` attribute.
 */
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
