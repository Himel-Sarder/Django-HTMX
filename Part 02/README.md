## **Part 2: HTMX Basics & First Interaction**

> In this part, you'll create your **first HTMX interaction**: a button that loads a partial view into the page **without reloading**.

### Goal:

* Use `hx-get`, `hx-target`, and `hx-swap`
* Understand how HTMX communicates with Django
* Load a small HTML block (a partial) dynamically

### What we’ll Build:

On the home page, you’ll click a **“Load Welcome Message”** button, and HTMX will fetch the message from a Django view and insert it into the page — **without reloading**.

### Inside the content block:

```html
<h1 class="text-3xl font-bold mb-4">Welcome to TaskForge </h1>
```

* A heading with some Tailwind CSS classes for styling.

### The HTMX Button:

```html
<button 
    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded transition"
    hx-get="{% url 'load-welcome' %}" 
    hx-target="#welcome-box"
    hx-swap="innerHTML">
    Load Welcome Message
</button>
```

* `hx-get="{% url 'load-welcome' %}"`: When clicked, HTMX sends a GET request to the URL named `load-welcome` (resolved by Django).
* `hx-target="#welcome-box"`: The server response will be inserted inside the element with ID `welcome-box`.
* `hx-swap="innerHTML"`: Replace the **inside** content of `#welcome-box` with the response HTML.
* The button is styled with Tailwind CSS for blue background, hover effect, padding, rounded corners, and smooth transition.

### Breaking it down:

#### 1. **`hx-get`**

* This is an **HTMX attribute**.
* It tells HTMX to make an **HTTP GET request** to a specified URL **when the element is triggered** (by default, on a click).
* HTMX then fetches the response from that URL and injects it into the page based on other attributes like `hx-target` and `hx-swap`.

#### 2. **`{% url 'load-welcome' %}`**

* This is a **Django template tag**.
* It dynamically **generates the URL** for a named URL pattern.
* `'load-welcome'` is the **name of a URL pattern** defined in your Django app's `urls.py`.

For example, in your `boards/urls.py` you have:

```python
path('load-welcome/', views.welcome_partial, name='load-welcome'),
```

* This means `{% url 'load-welcome' %}` outputs the string `/load-welcome/` (or the full path relative to your domain).

### What happens at runtime?

* When Django renders your template, it replaces `{% url 'load-welcome' %}` with `/load-welcome/`.
* So your button’s attribute becomes:

```html
hx-get="/load-welcome/"
```

* When you click the button, HTMX sends a **GET request to `/load-welcome/`**.
* The server responds with HTML, which HTMX then inserts into the page (inside the element identified by `hx-target`).

### Why use `{% url %}` instead of hardcoding URLs?

* It **avoids hardcoding paths** in your templates.
* If you change your URL patterns later, your templates don’t break.
* It keeps URL management **DRY and consistent** across the project.


### Summary:

`hx-get="{% url 'load-welcome' %}"` means:

> “When triggered, make an HTMX GET request to the Django URL named `'load-welcome'`.”

---
### The Target Container:

```html
<div id="welcome-box" class="mt-4"></div>
```

* This empty `div` is where the partial HTML returned by the `load-welcome` view will be inserted.
* Initially empty, it gets filled only when you click the button.
