document.querySelectorAll('[data-editorial-atlas]').forEach((atlas) => {
  const nodes = Array.from(atlas.querySelectorAll('[data-node]'));
  const edges = Array.from(atlas.querySelectorAll('[data-connects]'));
  const title = atlas.querySelector('[data-atlas-title]');
  const description = atlas.querySelector('[data-atlas-description]');
  const defaultTitle = title?.textContent || '';
  const defaultDescription = description?.textContent || '';

  const clearActiveState = () => {
    atlas.classList.remove('has-active');
    nodes.forEach((node) => node.classList.remove('is-active'));
    edges.forEach((edge) => edge.classList.remove('is-active'));

    if (title) {
      title.textContent = defaultTitle;
    }
    if (description) {
      description.textContent = defaultDescription;
    }
  };

  const setActiveState = (node) => {
    const nodeId = node.dataset.node;
    atlas.classList.add('has-active');

    nodes.forEach((item) => item.classList.toggle('is-active', item === node));
    edges.forEach((edge) => {
      const connectedNodes = (edge.dataset.connects || '').split(/\s+/);
      edge.classList.toggle('is-active', connectedNodes.includes(nodeId));
    });

    if (title) {
      title.textContent = node.dataset.title || defaultTitle;
    }
    if (description) {
      description.textContent = node.dataset.description || defaultDescription;
    }
  };

  nodes.forEach((node) => {
    node.addEventListener('mouseenter', () => setActiveState(node));
    node.addEventListener('focus', () => setActiveState(node));

    node.addEventListener('mouseleave', () => {
      if (!atlas.contains(document.activeElement)) {
        clearActiveState();
      }
    });

    node.addEventListener('blur', () => {
      window.requestAnimationFrame(() => {
        const focusedNode = document.activeElement?.closest?.('[data-node]');
        if (focusedNode && atlas.contains(focusedNode)) {
          setActiveState(focusedNode);
          return;
        }
        clearActiveState();
      });
    });
  });

  atlas.addEventListener('mouseleave', () => {
    if (!atlas.contains(document.activeElement)) {
      clearActiveState();
    }
  });

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if ('IntersectionObserver' in window && !prefersReducedMotion) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        atlas.classList.add('is-visible');
        observer.unobserve(atlas);
      });
    }, { threshold: 0.2 });

    observer.observe(atlas);
  } else {
    atlas.classList.add('is-visible');
  }
});
