document.querySelectorAll('[data-editorial-constellation]').forEach((constellation) => {
  const nodes = Array.from(constellation.querySelectorAll('[data-node]'));
  const edges = Array.from(constellation.querySelectorAll('[data-edge]'));
  const title = constellation.querySelector('[data-constellation-title]');
  const description = constellation.querySelector('[data-constellation-description]');
  const defaultTitle = title?.textContent || '';
  const defaultDescription = description?.textContent || '';

  const clearActiveState = () => {
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
    nodes.forEach((item) => item.classList.toggle('is-active', item === node));
    edges.forEach((edge) => edge.classList.toggle('is-active', edge.dataset.edge === nodeId));
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
      if (!constellation.contains(document.activeElement)) {
        clearActiveState();
      }
    });
    node.addEventListener('blur', () => {
      window.requestAnimationFrame(() => {
        const focusedNode = document.activeElement?.closest?.('[data-node]');
        if (focusedNode && constellation.contains(focusedNode)) {
          setActiveState(focusedNode);
          return;
        }
        clearActiveState();
      });
    });
  });

  constellation.addEventListener('mouseleave', () => {
    if (!constellation.contains(document.activeElement)) {
      clearActiveState();
    }
  });

  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) {
          return;
        }
        constellation.classList.add('is-visible');
        observer.unobserve(constellation);
      });
    }, { threshold: 0.28 });
    observer.observe(constellation);
  } else {
    constellation.classList.add('is-visible');
  }
});
