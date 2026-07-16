import numpy
import create_dots
import graph
running = True
paused = False
count=0
while running:
    # 处理事件（只处理退出和按键状态变化）
    for event in graph.pygame.event.get():
        if event.type == graph.QUIT:
            running = False
        elif event.type == graph.pygame.KEYDOWN:
            if event.key == graph.pygame.K_p:
                paused= not paused
    if not paused:
        create_dots.unv.main()
    graph.step(create_dots.unv)
    