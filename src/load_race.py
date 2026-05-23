import fastf1

# Enable cache
fastf1.Cache.enable_cache('cache')

# Load session
session = fastf1.get_session(2024, 'Monaco', 'Q')
session.load()

# Pick fastest laps
lec = session.laps.pick_driver('LEC').pick_fastest()
ver = session.laps.pick_driver('VER').pick_fastest()

# Print sector times
print("=== LECLERC ===")
print("Sector 1:", lec['Sector1Time'])
print("Sector 2:", lec['Sector2Time'])
print("Sector 3:", lec['Sector3Time'])

print("\n=== VERSTAPPEN ===")
print("Sector 1:", ver['Sector1Time'])
print("Sector 2:", ver['Sector2Time'])
print("Sector 3:", ver['Sector3Time'])

# Compare sectors
print("\n=== COMPARISON ===")

if lec['Sector1Time'] < ver['Sector1Time']:
    print("Leclerc faster in Sector 1")
else:
    print("Verstappen faster in Sector 1")

if lec['Sector2Time'] < ver['Sector2Time']:
    print("Leclerc faster in Sector 2")
else:
    print("Verstappen faster in Sector 2")

if lec['Sector3Time'] < ver['Sector3Time']:
    print("Leclerc faster in Sector 3")
else:
    print("Verstappen faster in Sector 3")