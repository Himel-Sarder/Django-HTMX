![image](https://github.com/user-attachments/assets/47e6d5da-de7f-411d-b594-0541ee2a1f52)

```html
<button
    hx-delete="{% url 'delete-task' task.id %}"
    hx-target="#list-{{ task.list.id }}-tasks"
    hx-swap="outerHTML"
    hx-confirm="Are you sure you want to delete this task?"
    class="text-red-600 font-bold hover:text-red-800 ml-4"
>×</button>
```


### `hx-delete="{% url 'delete-task' task.id %}"`

* **What it does**: Sends a `DELETE` request to the Django URL that deletes the task with `task.id`.
* **How it works**: HTMX treats this as an AJAX-style request — you don’t need a form.
* **Django tag**: `{% url 'delete-task' task.id %}` resolves to something like `/tasks/3/delete/`.

---

### `hx-target="#list-{{ task.list.id }}-tasks"`

* **What it does**: Tells HTMX **where** to update content after the delete request succeeds.
* This should match the ID of the `<div>` that holds the **task list** for that board/list.

```html
<div id="list-1-tasks"> <!-- This is what gets replaced -->
  ...
</div>
```

So after deletion, HTMX will replace that entire `div` with the updated list of tasks (as returned by the Django view).


### `hx-swap="outerHTML"`

* **What it does**: Specifies how HTMX should update the `hx-target` element.
* `outerHTML` means: **Replace the entire targeted element** (not just its contents).

Here, it replaces the task list container (`#list-X-tasks`) with fresh HTML after deletion.


### `hx-confirm="Are you sure you want to delete this task?"`

* **What it does**: Shows a browser confirmation dialog before sending the DELETE request.
* If user clicks "Cancel", the request is **not** sent.
* Great for preventing accidental deletions.


### `class="text-red-600 font-bold hover:text-red-800 ml-4"`

* **Tailwind CSS classes** for styling:

  * `text-red-600`: Makes the delete icon red
  * `font-bold`: Bolds the text (the ×)
  * `hover:text-red-800`: Makes the red darker on hover
  * `ml-4`: Adds left margin (spacing from the task text)


### Content of the Button: `×`

* This is the delete symbol (multiplication sign), often used for "close" or "remove".
* You could replace it with a trash icon (like `<i class="fas fa-trash"></i>`) if you’re using FontAwesome or Heroicons.


## What Happens When You Click the Button:

1. You’re asked: *"Are you sure you want to delete this task?"*
2. If you confirm, HTMX sends a `DELETE` request to the Django view.
3. Django deletes the task and returns the updated HTML fragment (e.g. all tasks in that list).
4. HTMX takes that response and **replaces the entire task list container** with the new version.
