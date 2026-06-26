return {
  separator = "|",

  left = {
    {
      name = "mode",
      fmt = function(str)
        return str:sub(1,1)
      end,
    },
    {
      name = "state",
      fmt = function(str)
        if str == "TOCANDO" then
          return "TOCANDO ▶"
        elseif str == "PAUSA" then
          return "PAUSA ⏸"
        else 
          return str
        end
      end,
    },
    {
      name = "song",
      fmt = function(str)
        return "["..str.."]"
      end,
    },
  },
  right = {
    {
      name = "position"
    }
  }
}
