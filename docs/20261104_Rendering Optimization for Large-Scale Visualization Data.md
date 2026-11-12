# [Weekly 5-Min Tech Talk] Rendering Optimization for Large-Scale Visualization Data

<table>
  <tbody><tr><td><b>Presenter</b></td><td>Sujee Cho</td></tr></tbody>
  <tbody><tr><td><b>Date</b></td><td>2026-11-04</td></tr></tbody>
  <tbody><tr><td><b>Keywords</b></td><td>Rendering, Performance, Quadtree, LOD, WebGL</td></tr></tbody>
</table>

---

## 1. TL;DR
Overcame the browser's performance limits when visualizing and rendering 500K+ data points by combining Quadtree-based spatial partitioning in WebGL with LOD-based detail reduction.

Offloaded heavy rendering work from the CPU (JavaScript main thread) to the GPU.

Applied a simple rendering philosophy in practice: "Don't draw what isn't visible, and cluster what matters less."
## 2. Problem & Background
- Limits of DOM and standard Canvas: Rendering around 500K data points caused severe memory overload and frame drops.
- Root cause of the bottleneck: Data outside the user's visible screen was still included in rendering computations, blocking the browser's main thread.

## 3. Solution & Architecture
- Quadtree: Skipping rendering through spatial partitioning
    - Introduced a tree structure that recursively divides the entire screen into four quadrants.
    - Regions that don't intersect the user's current viewport are culled from the rendering tree entirely, minimizing unnecessary computation.
    ![quadtree visualization](./assets/quadtree.jpeg)
        
- A 4-layer rendering pipeline to sustain 60 FPS (with LOD)
    - Designed a 4-layer architecture from initial JSON data to on-screen rendering, preserving data integrity and maintaining 60 FPS during user interaction.
    1. **Data Layer:**
        - Builds a Quadtree from the JSON data and precomputes the diameter of each element to render.
        - Converts the data into SoA (Structure of Arrays) typed arrays optimized for GPU computation and memory access.
    2. **SSoT State Caching Layer:**
        - Stores parsed data in a global store that serves as the Single Source of Truth (SSoT).
        - Topic index cache: Caches results on the first view switch so repeated requests don't trigger redundant re-parsing.
    3. **Adaptive Layer:**
        - Performs Quadtree-based viewport culling on every user event.
        - Evaluates the density of visible data and selects the final key data to render within each grid cell (weight-based LOD).
        ![LOD comparison](./assets/LOD_comparison.png)
        
    4. **GPU Rendering Layer:**
        - Processes the final filtered data in parallel using custom WebGL 2.0 shaders.
        - Renders tens of thousands of semi-transparent overlapping data points (overdraw) without bottlenecks by utilizing Index Buffers and Fixed-Function Blending.

## 4. Practical Takeaways
- 2D extension of virtual scrolling: The principle behind a Quadtree can be viewed as extending virtual scrolling—which removes off-screen list items from the DOM—into two dimensions.
- Data clustering strategy: When building complex dashboards or high-density chart UIs, this architecture can be applied to group data and defer off-viewport computations to reduce initial loading overhead.

## 5. Glossary & FAQ

### Glossary
- **Index Buffer**
    - Reduces the data "shipped" to the GPU.
    - Instead of sending the coordinates of 6 vertices (2 triangles) to the GPU every time a rectangle is drawn, it stores vertices 0, 1, 2, and 3 once and instructs the GPU: "Combine them in the order of these numbered tickets (indices)."
- **Fixed-Function Blending**
    - Calculates the final pixel color of tens of thousands of overlapping semi-transparent data points directly in the frontend code or heavy shader operations, rather than using WebGL's built-in hardware functions like `gl.blendFunc()`.
    - Sustains 60 FPS even with tens of thousands of overlapping elements (overdraw) because GPU hardware units compute transparency in parallel at the chipset level.
- **Overdraw**
    - A phenomenon where dozens or hundreds of semi-transparent data points are drawn overlapping on the exact same pixel position on screen.
    - In the DOM or Canvas 2D, the CPU has to calculate the resulting color (alpha blending) one by one whenever transparent colors overlap, causing rendering to slow down exponentially as data clusters together.
- **Virtual Scroll (Lazy building)**
    - An approach that avoids drawing all 10,000 DOM elements or widgets when displaying a 10,000-item list. Instead, it calculates the vertical scroll position to render only the ~20 items currently visible on screen, skipping items outside the viewport above and below.
    - React (DOM): Adopt external libraries such as `react-window` or `react-virtualized`.
    - Flutter: Using a `Column` inside a `SingleChildScrollView` renders all off-screen widgets at once, whereas `ListView.builder` builds them lazily on demand.

### FAQ
- **Q1. Is there a specific threshold for the number of data points where we should switch from DOM or Canvas 2D to WebGL?**
    - **A:** WebGL isn't always the answer. If you have fewer than 10,000 data points or minimal visual overlap (overdraw), easier-to-maintain options like Canvas 2D or existing libraries like ECharts are much better. However, once data exceeds tens of thousands of points and semi-transparent markers start clustering in one area, CPU-based alpha blending can no longer keep up—that's when you should consider offloading computation to the GPU via WebGL.
- **Q2. Isn't the initial step of partitioning and computing all the data into a Quadtree (Data Layer) heavy enough to block the main thread on its own?**
    - **A:** Building the Quadtree during the initial render is indeed quite heavy. To mitigate this, it is computed only once and stored in the **SSoT State Caching Layer**, preventing redundant recalculations when switching views. If initial load performance needs to be improved even further, the tree construction step can be offloaded to a Web Worker so it runs on a background thread.
- **Q3. In LOD (detail reduction), you mentioned culling "less important data." How did you define the criteria for importance?**
    - **A:** Since my paper dealt with sentiment analysis data, points with the highest "sentiment weight" were kept as key data. In production, you can cluster data using business metrics that users need to notice first when zoomed out—such as most recent activity date, error severity, or log frequency—as weights.
- **Q4. Writing custom WebGL 2.0 shaders from scratch seems complex for frontend work. Are there practical libraries we can use more easily in production?**
    - **A:** In production, I recommend evaluating WebGL-based visualization libraries like `deck.gl` or `PixiJS` first. In this research, however, we built a custom shader pipeline from scratch because we needed a specialized 4-level LOD architecture to finely control dense sentiment distributions across 500K data points.

## 6. References
- [quadtree](https://www.linkedin.com/posts/fernando-franco-4696708_what-is-a-quadtree-a-quadtree-is-a-data-activity-7317833959915089922-dIEa)
