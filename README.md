1. **Requisitos**

* PHP >= 8.0 (recomendado 8.1+)
* cURL habilitado (viene por defecto en la mayoría de instalaciones)

2. **Instalación**

<pre class="overflow-visible!" data-start="6137" data-end="6193"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span># clona tu repo y copia index.php en la raíz</span><span>
</span></span></code></div></div></pre>

3. **Ejecutar en puerto 5000**

<pre class="overflow-visible!" data-start="6226" data-end="6267"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span>php -S 0.0.0.0:5000 index.php
</span></span></code></div></div></pre>

> El archivo `index.php` actúa como router del servidor embebido de PHP.

4. **Probar con curl**

<pre class="overflow-visible!" data-start="6366" data-end="6563"><div class="contain-inline-size rounded-2xl relative bg-token-sidebar-surface-primary"><div class="sticky top-9"><div class="absolute end-0 bottom-0 flex h-9 items-center pe-2"><div class="bg-token-bg-elevated-secondary text-token-text-secondary flex items-center gap-4 rounded-sm px-2 font-sans text-xs"><span class="" data-state="closed"></span></div></div></div><div class="overflow-y-auto p-4" dir="ltr"><code class="whitespace-pre! language-bash"><span><span># Categorías</span><span>
curl http://localhost:5000/categories

</span><span># Chiste por categoría (ej: "dev")</span><span>
curl http://localhost:5000/joke/dev

</span><span># Búsqueda</span><span>
curl </span><span>"http://localhost:5000/search?query=database"</span><span>
</span></span></code></div></div></pre>
