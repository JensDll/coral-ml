using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Domain.Entities
{
    public class FormFileZipEntry
    {
        public string EntryName { get; set; }

        public IFormFile File { get; set; }
    }
}
