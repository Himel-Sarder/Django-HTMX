## **Part 2: HTMX Basics & First Interaction**

> In this part, you'll create your **first HTMX interaction**: a button that loads a partial view into the page **without reloading**.

---

### Goal:

* Use `hx-get`, `hx-target`, and `hx-swap`
* Understand how HTMX communicates with Django
* Load a small HTML block (a partial) dynamically

---

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

### The Target Container:

```html
<div id="welcome-box" class="mt-4"></div>
```

* This empty `div` is where the partial HTML returned by the `load-welcome` view will be inserted.
* Initially empty, it gets filled only when you click the button.
