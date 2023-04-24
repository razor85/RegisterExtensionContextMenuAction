import sys
import winreg

if len(sys.argv) < 4:
  print('Usage: {} Extension CommandName Command\n  Example: {} txt "Open with Neovim" "c:\\\\neovim\\\\neovim.exe ""%%1"""'.format(sys.argv[0], sys.argv[0]))
  sys.exit(0)

extensionToRegister, commandName, exeCommand = sys.argv[1:]

print('Extension to register: {}'.format(extensionToRegister))
print('Command Name: {}'.format(commandName))
print('Command: {}'.format(exeCommand))
print('Continue (Y/N)?', end=None)

answer = sys.stdin.read(1)
if answer is None or answer.lower() != 'y':
  print('Aborting')
  sys.exit(0)

msgPath = 'Computer\HKEY_CLASSES_ROOT\SystemFileAssociations'

assocKey = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "SystemFileAssociations")
if assocKey is None:
  print('Failed to open {}'.format(msgPath))
  sys.exit(0)

extKey = winreg.CreateKey(assocKey, '.{}'.format(extensionToRegister))
if extKey is None:
  msgPath += '\\.{}'.format(extensionToRegister)
  print('Failed to create {}'.format(msgPath))
  sys.exit(0)

shellKey = winreg.CreateKey(extKey, 'shell')
if shellKey is None:
  msgPath += '\\shell'
  print('Failed to create {}'.format(msgPath))
  sys.exit(0)

commandNameKey = winreg.CreateKey(shellKey, commandName)
if commandNameKey is None:
  msgPath += '\\{}'.format(commandName)
  print('Failed to create {}'.format(msgPath))
  sys.exit(0)

commandKey = winreg.CreateKey(commandNameKey, 'command')
if commandNameKey is None:
  msgPath += '\\command'
  print('Failed to create {}'.format(msgPath))
  sys.exit(0)

winreg.SetValue(commandKey, '', winreg.REG_SZ, exeCommand)
print('Done!')