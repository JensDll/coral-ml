using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Contracts.Response
{
    public class TFLiteModelResponseDto
    {
        public int Id { get; set; }

        public string ModelName { get; set; }

        public byte[] Model { get; set; }
    }
}
