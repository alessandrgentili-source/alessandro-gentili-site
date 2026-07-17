document.querySelectorAll('[data-system-map]').forEach((map) => {
  const nodes = Array.from(map.querySelectorAll('[data-node-id]'));
  const edges = Array.from(map.querySelectorAll('[data-from][data-to]'));
  const title = map.querySelector('[data-system-title]');
  const description = map.querySelector('[data-system-description]');
  const defaultTitle = title?.textContent || '';
  const defaultDescription = description?.textContent || '';

  nodes.forEach((node) => {
    if (!node.matches('a, button, input, select, textarea, [tabindex]')) {
      node.tabIndex = 0;
      node.setAttribute('role', 'button');
    }
  });

  const clearActiveState = () => {
    map.classList.remove('has-active');
    nodes.forEach((node) => node.classList.remove('is-active', 'is-related'));
    edges.forEach((edge) => edge.classList.remove('is-active'));

    if (title) title.textContent = defaultTitle;
    if (description) description.textContent = defaultDescription;
  };

  const setActiveState = (activeNode) => {
    const activeId = activeNode.dataset.nodeId;
    const relatedIds = new Set([activeId]);

    edges.forEach((edge) => {
      const from = edge.dataset.from;
      const to = edge.dataset.to;
      const isRelevant = from === activeId || to === activeId;
      edge.classList.toggle('is-active', isRelevant);

      if (isRelevant) {
        relatedIds.add(from);
        relatedIds.add(to);
      }
    });

    map.classList.add('has-active');
    nodes.forEach((node) => {
      const nodeId = node.dataset.nodeId;
      node.classList.toggle('is-active', node === activeNode);
      node.classList.toggle('is-related', node !== activeNode && relatedIds.has(nodeId));
    });

    if (title) title.textContent = activeNode.dataset.title || defaultTitle;
    if (description) description.textContent = activeNode.dataset.description || defaultDescription;
  };

  nodes.forEach((node) => {
    node.addEventListener('mouseenter', () => setActiveState(node));
    node.addEventListener('focus', () => setActiveState(node));
    node.addEventListener('mouseleave', () => {
      if (!map.contains(document.activeElement)) clearActiveState();
    });
    node.addEventListener('blur', () => {
      window.requestAnimationFrame(() => {
        const focusedNode = document.activeElement?.closest?.('[data-node-id]');
        if (focusedNode && map.contains(focusedNode)) {
          setActiveState(focusedNode);
          return;
        }
        clearActiveState();
      });
    });
  });

  map.addEventListener('mouseleave', () => {
    if (!map.contains(document.activeElement)) clearActiveState();
  });

  map.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      document.activeElement?.blur?.();
      clearActiveState();
    }
  });
});
