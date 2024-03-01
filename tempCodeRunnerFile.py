for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change -= 0.3
            elif event.key == pygame.K_RIGHT:
                x_change += 0.3
            elif event.key == pygame.K_SPACE:
                if b_state == "ready":
                    bullet_sound = mixer.Sound("audio/lazer.mp3")
                    bullet_sound.play()
                    bulletx = playerx
                    fire_bullet(bulletx, bullety)
            elif event.key == pygame.K_p:
                    paused = not paused        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                x_change = 0