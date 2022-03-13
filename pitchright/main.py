import multiprocessing
multiprocessing.freeze_support()

try:
    import pyi_splash
    pyi_splash.close()
except:
    pass

if __name__ == "__main__":
    from pitchright.game import PitchRight
    p = PitchRight(1920, 1080)
    p.start()