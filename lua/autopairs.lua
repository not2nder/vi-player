local M = {}

local pairs = {
  ["("] = ")",
  ["["] = "]",
  ["{"] = "}",
  ['"'] = '"'
}

local closed = {
  [")"] = true, 
  ["]"] = true,
  ["}"] = true,
  ['"'] = true
}

function M.on_key(ctx, key)
  if ctx.mode ~= "COMMAND" then
    return false
  end

  if pairs[key] ~= nil then
    ctx.text = string.sub(ctx.text, 1, ctx.cursor) .. key .. pairs[key] .. string.sub(ctx.text, ctx.cursor+1)
    ctx.cursor = ctx.cursor + 1
    return true

  elseif key == ctx.text[ctx.cursor] then 
    if closed[key] ~= nil then
      ctx.cursor = ctx.cursor + 2
      return true
    end
    return false
  end
  return false
end

return M
