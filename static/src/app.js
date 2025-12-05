/**
 * Project:     conneCTION
 * Name:        static/src/app.js
 * Author:      Ian Kollipara <ikollipara2@huskers.unl.edu>
 * Date:        2025-11-12
 * Description: Main Frontend Entrypoint
 */

import "./scss/app.scss";
import * as Turbo from "@hotwired/turbo";
import { Application } from "@hotwired/stimulus";

window.Turbo = Turbo;

Turbo.start();

window.Stimulus = Application.start();

Promise.all([
  import("./controllers/combobox_controller"),
  import("./controllers/editor_controller"),
  import("./controllers/quill_controller"),
  import("./controllers/submit_form_controller"),
  import("./controllers/dialog_controller"),
  import("./controllers/frame_reload_controller"),
  import("./controllers/post_display_controller"),
  import("./controllers/remove_me_controller"),
]).then(
  ([
    { default: ComboBoxController },
    { default: EditorController },
    { default: QuillController },
    { default: SubmitFormController },
    { default: DialogController },
    { default: FrameReloadController },
    { default: PostDisplayController },
    { default: RemoveMeController },
  ]) => {
    Stimulus.register("combo-box", ComboBoxController);
    Stimulus.register("editor", EditorController);
    Stimulus.register("quill", QuillController);
    Stimulus.register("submit-form", SubmitFormController);
    Stimulus.register("dialog", DialogController);
    Stimulus.register("frame-reload", FrameReloadController);
    Stimulus.register("post-display", PostDisplayController);
    Stimulus.register("remove-me", RemoveMeController);
  },
);
