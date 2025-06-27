```html
<form
    hx-post="{% url 'add-task' list_id %}"
    hx-target="#list-{{ list_id }}-tasks"
    hx-swap="beforeend"
    class="space-y-2 mt-3"
    method="POST"
>
```

---

### 1. `hx-post="{% url 'add-task' list_id %}"`

* **HTMX attribute**: `hx-post` sends a POST request to the specified URL when the form is submitted.
* **Django template tag**: `{% url 'add-task' list_id %}` resolves to something like `/lists/1/add-task/` dynamically.
* This replaces the standard `action="/some-url"` and enables HTMX behavior.

**Goal**: Tell HTMX to send the form data to Django's `add_task` view **via POST**.

---

### 2. `hx-target="#list-{{ list_id }}-tasks"`

* This tells HTMX **where to place the server's response** (usually HTML).
* `#list-1-tasks`, `#list-2-tasks`, etc., are the dynamic divs under each list that show the tasks.

 **Goal**: Inject the newly created task HTML into the correct list’s container.

---

### 3. `hx-swap="beforeend"`

* Controls **how** the response is inserted into the target.
* `beforeend` means: “Append the new HTML to the end of the target div.”

 **Goal**: Add the new task **at the bottom** of the task list.

---

### 4. `class="space-y-2 mt-3"`

* Tailwind CSS utility classes:

  * `space-y-2`: Adds vertical space (margin) between child elements.
  * `mt-3`: Adds top margin to the form for spacing from above elements.

 **Goal**: Visually space out the form nicely.

---

### 5. `method="POST"`

* Standard HTML attribute that tells the browser (and HTMX) this is a `POST` form.
* Required for CSRF and form submission to work in Django.

 **Goal**: Ensure Django accepts the data and checks CSRF properly.
