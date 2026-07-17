document.querySelectorAll('[data-system-map]').forEach((map) => {
  const nodes = Array.from(map.querySelectorAll('[data-node-id]'));
  const edges = Array.from(map.querySelectorAll('[data-from][data-to]'));
  const title = map.querySelector('[data-system-title]');
  const description = map.querySelector('[data-system-description]');
  const defaultTitle = title?.textContent || '';
  const defaultDescription = description?.textContent || '';

  const nodeById = new Map(
    nodes.map((node) => [node.dataset.nodeId, node])
  );

  nodes.forEach((node) => {
    if (!node.matches('a, button, [tabindex]')) {
      node.tabIndex = 0;
    }
  });

  const clearActiveState = () => {
    map.classList.remove('has-active');
    nodes.forEach((node) => {
      node.classList.remove('is-active', 'is-related');
    });
    edges.forEach((edge) => edge.classList.remove('is-active'));

    if (title) {
      title.textContent = defaultTitle;
    }
    if (description) {
      description.textContent = defaultDescription;
    }
  };

  const setActiveState = (node) => {
    const nodeId = node.dataset.nodeId;
    const relatedIds = new Set([nodeId]);

    map.classList.add('has-active');

    edges.forEach((edge) => {
      const isConnected = edge.dataset.from === nodeId || edge.dataset.to === nodeId;
      edge.classList.toggle('is-active', isConnected);

      if (isConnected) {
        relatedIds.add(edge.dataset.from);
        relatedIds.add(edge.dataset.to);
      }
    });

    nodes.forEach((item) => {
      item.classList.toggle('is-active', item === node);
      item.classList.toggle('is-related', relatedIds.has(item.dataset.nodeId));
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
      if (!map.contains(document.activeElement)) {
        clearActiveState();
      }
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
    if (!map.contains(document.activeElement)) {
      clearActiveState();
    }
  });

  map.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      clearActiveState();
      document.activeElement?.blur?.();
    }
  });

  const invalidRelations = edges.filter((edge) => (
    !nodeById.has(edge.dataset.from) || !nodeById.has(edge.dataset.to)
  ));

  if (invalidRelations.length) {
    console.warn('Editorial system map: unresolved relation endpoints.', invalidRelations);
  }
});
