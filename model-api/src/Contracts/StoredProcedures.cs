using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Contracts
{
    public static class StoredProcedures
    {
        public static class TFLiteRecord
        {
            public const string Prefix = "spTFLiteRecord_";

            public const string GetAll = Prefix + "GetAll";

            public const string GetById = Prefix + "GetById";

            public const string Create = Prefix + "Create";

            public const string Delete = Prefix + "Delete";
        }
    }
}
