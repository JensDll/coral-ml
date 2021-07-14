using Application.Data.DataTransfer;
using Application.Data.DataTransfer.RecordType;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Data.Repositories
{
    public interface IRecordTypeRepository
    {
        public Task<EnumerableEnevelope<RecordTypeGetAll>> GetAllAsync();
    }
}
