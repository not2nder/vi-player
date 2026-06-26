return {
  options = {},
  sections = {
    -- esquerda
    lualine_a = {
      {
        name = "mode",
        fmt = function(str)
          return str:sub(1,1)
        end,
      }
    },

    lualine_b = {
      {
        name = "state",
        fmt = function(str)
          if str == "TOCANDO" then
            return str.." "
          elseif str == "PAUSA" then
            return str.." "
          end
        end
      }
    },

    lualine_c = {
      {
        name = "song",
      },
      {
        name = "artist",
        fmt = function(str)
          if str ~= "" then
            return "["..str.."]"
          end
        end
      }
    },

    -- direita
    lualine_x = {
      {
        name = "theme",
        fmt = function(str)
          return "tema: "..str
        end,
      }
    },
    lualine_y = {
      {
        name="position"
      },
      {
        name = "percent"
      }
    },
    lualine_z = {}, 
  }
}
