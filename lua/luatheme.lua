local M = {}

math.randomseed(os.time())

function M.current()
  vi.ui.message("Tema atual: '"..vi.theme.current().."'")
end

function M.random()
  local old = vi.theme.current()
  local themelist = vi.theme.list()
  local chosen = themelist[math.random(#themelist)]
  
  if chosen == old then
    chosen = themelist[math.random(#themelist)]
  end

  vi.theme.set(chosen)
  vi.ui.message("Tema atual: " .. chosen)
end

function M.count()
  local themes = vi.theme.list()
  vi.ui.message(#themes .. " Temas em ~/.config/vi-player/themes")
end

function M.grep(text)
  local themes = vi.theme.list()

  for _, name in ipairs(themes) do
    if string.find(name, text,1) then
      vi.theme.set(name)
      vi.ui.message("Tema: '".. name .."'")
      return
    end
  end
  vi.ui.message("Sem correspondências para '"..text.."'")
end

return M
